﻿#pragma checksum "..\..\..\Views\AdminWindow.xaml" "{8829d00f-11b8-4213-878b-770e8597ac16}" "C45F0CF956CE523FFC4BD8CD171F9E258CCFFC2B433EA2F78BD4CA1A9A7CE2C4"
//------------------------------------------------------------------------------
// <auto-generated>
//     Этот код создан программой.
//     Исполняемая версия:4.0.30319.42000
//
//     Изменения в этом файле могут привести к неправильной работе и будут потеряны в случае
//     повторной генерации кода.
// </auto-generated>
//------------------------------------------------------------------------------

using System;
using System.Diagnostics;
using System.Windows;
using System.Windows.Automation;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Markup;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Effects;
using System.Windows.Media.Imaging;
using System.Windows.Media.Media3D;
using System.Windows.Media.TextFormatting;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Shell;


namespace SkladApp.Views {
    
    
    /// <summary>
    /// AdminWindow
    /// </summary>
    public partial class AdminWindow : System.Windows.Window, System.Windows.Markup.IComponentConnector {
        
        
        #line 11 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.TextBlock UserInfoTextBlock;
        
        #line default
        #line hidden
        
        
        #line 12 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.TabControl TabControl;
        
        #line default
        #line hidden
        
        
        #line 15 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid UsersDataGrid;
        
        #line default
        #line hidden
        
        
        #line 20 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid ProductsDataGrid;
        
        #line default
        #line hidden
        
        
        #line 25 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid StorageLocationsDataGrid;
        
        #line default
        #line hidden
        
        
        #line 30 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid CustomersDataGrid;
        
        #line default
        #line hidden
        
        
        #line 35 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid OrdersDataGrid;
        
        #line default
        #line hidden
        
        
        #line 40 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid OrderDetailsDataGrid;
        
        #line default
        #line hidden
        
        
        #line 45 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid InvoicesDataGrid;
        
        #line default
        #line hidden
        
        
        #line 50 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid InvoiceDetailsDataGrid;
        
        #line default
        #line hidden
        
        
        #line 55 "..\..\..\Views\AdminWindow.xaml"
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1823:AvoidUnusedPrivateFields")]
        internal System.Windows.Controls.DataGrid SuppliersDataGrid;
        
        #line default
        #line hidden
        
        private bool _contentLoaded;
        
        /// <summary>
        /// InitializeComponent
        /// </summary>
        [System.Diagnostics.DebuggerNonUserCodeAttribute()]
        [System.CodeDom.Compiler.GeneratedCodeAttribute("PresentationBuildTasks", "4.0.0.0")]
        public void InitializeComponent() {
            if (_contentLoaded) {
                return;
            }
            _contentLoaded = true;
            System.Uri resourceLocater = new System.Uri("/SkladApp;component/views/adminwindow.xaml", System.UriKind.Relative);
            
            #line 1 "..\..\..\Views\AdminWindow.xaml"
            System.Windows.Application.LoadComponent(this, resourceLocater);
            
            #line default
            #line hidden
        }
        
        [System.Diagnostics.DebuggerNonUserCodeAttribute()]
        [System.CodeDom.Compiler.GeneratedCodeAttribute("PresentationBuildTasks", "4.0.0.0")]
        [System.ComponentModel.EditorBrowsableAttribute(System.ComponentModel.EditorBrowsableState.Never)]
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Design", "CA1033:InterfaceMethodsShouldBeCallableByChildTypes")]
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Maintainability", "CA1502:AvoidExcessiveComplexity")]
        [System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1800:DoNotCastUnnecessarily")]
        void System.Windows.Markup.IComponentConnector.Connect(int connectionId, object target) {
            switch (connectionId)
            {
            case 1:
            this.UserInfoTextBlock = ((System.Windows.Controls.TextBlock)(target));
            return;
            case 2:
            this.TabControl = ((System.Windows.Controls.TabControl)(target));
            
            #line 12 "..\..\..\Views\AdminWindow.xaml"
            this.TabControl.SelectionChanged += new System.Windows.Controls.SelectionChangedEventHandler(this.TabControl_SelectionChanged);
            
            #line default
            #line hidden
            return;
            case 3:
            this.UsersDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 15 "..\..\..\Views\AdminWindow.xaml"
            this.UsersDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 4:
            this.ProductsDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 20 "..\..\..\Views\AdminWindow.xaml"
            this.ProductsDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 5:
            this.StorageLocationsDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 25 "..\..\..\Views\AdminWindow.xaml"
            this.StorageLocationsDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 6:
            this.CustomersDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 30 "..\..\..\Views\AdminWindow.xaml"
            this.CustomersDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 7:
            this.OrdersDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 35 "..\..\..\Views\AdminWindow.xaml"
            this.OrdersDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 8:
            this.OrderDetailsDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 40 "..\..\..\Views\AdminWindow.xaml"
            this.OrderDetailsDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 9:
            this.InvoicesDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 45 "..\..\..\Views\AdminWindow.xaml"
            this.InvoicesDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 10:
            this.InvoiceDetailsDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 50 "..\..\..\Views\AdminWindow.xaml"
            this.InvoiceDetailsDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 11:
            this.SuppliersDataGrid = ((System.Windows.Controls.DataGrid)(target));
            
            #line 55 "..\..\..\Views\AdminWindow.xaml"
            this.SuppliersDataGrid.MouseDoubleClick += new System.Windows.Input.MouseButtonEventHandler(this.DataGrid_MouseDoubleClick);
            
            #line default
            #line hidden
            return;
            case 12:
            
            #line 60 "..\..\..\Views\AdminWindow.xaml"
            ((System.Windows.Controls.Button)(target)).Click += new System.Windows.RoutedEventHandler(this.AddButton_Click);
            
            #line default
            #line hidden
            return;
            }
            this._contentLoaded = true;
        }
    }
}

